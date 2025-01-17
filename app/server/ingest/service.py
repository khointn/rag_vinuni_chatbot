import logging
import tempfile
from pathlib import Path
from typing import AnyStr, BinaryIO

from llama_index import ServiceContext, StorageContext
from llama_index.node_parser import SentenceWindowNodeParser

from app.components.embedding.component import EmbeddingComponent
from app.components.ingest.component import get_ingestion_component
from app.components.llm.component import LLMComponent
from app.components.node_store.component import NodeStoreComponent
from app.components.vector_store.component import VectorStoreComponent
from app.server.ingest.schemas import IngestedDoc

logger = logging.getLogger(__name__)


class IngestService:
    def __init__(
        self,
        llm_component: LLMComponent,
        vector_store_component: VectorStoreComponent,
        embedding_component: EmbeddingComponent,
        node_store_component: NodeStoreComponent,
    ) -> None:
        self.llm_service = llm_component
        self.storage_context = StorageContext.from_defaults(
            vector_store=vector_store_component.vector_store,
            docstore=node_store_component.doc_store,
            index_store=node_store_component.index_store,
        )
        node_parser = SentenceWindowNodeParser.from_defaults()
        self.ingest_service_context = ServiceContext.from_defaults(
            llm=self.llm_service.llm,
            embed_model=embedding_component.embedding_model,
            node_parser=node_parser,
            # Embeddings done early in the pipeline of node transformations, right
            # after the node parsing
            transformations=[node_parser, embedding_component.embedding_model],
        )

        self.ingest_component = get_ingestion_component(
            self.storage_context, self.ingest_service_context
        )

    def _ingest_data(self, file_name: str, file_data: AnyStr) -> list[IngestedDoc]:
        logger.debug(f"Got file data of size={len(file_data)} to ingest")
        # llama-index mainly supports reading from files, so
        # we have to create a tmp file to read for it to work
        # delete=False to avoid a Windows 11 permission error.
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            try:
                path_to_tmp = Path(tmp.name)
                if isinstance(file_data, bytes):
                    path_to_tmp.write_bytes(file_data)
                else:
                    path_to_tmp.write_text(str(file_data))
                return self.ingest_file(file_name, path_to_tmp)
            finally:
                tmp.close()
                path_to_tmp.unlink()

    def ingest_file(self, file_name: str, file_data: Path) -> list[IngestedDoc]:
        logger.info(f"Ingesting file_name={file_name}")
        documents = self.ingest_component.ingest(file_name, file_data)
        logger.info(f"Finished ingestion file_name={file_name}")
        return [IngestedDoc.from_document(document) for document in documents]

    def ingest_text(self, file_name: str, text: str) -> list[IngestedDoc]:
        logger.debug(f"Ingesting text data with file_name={file_name}")
        return self._ingest_data(file_name, text)

    def ingest_bin_data(
        self, file_name: str, raw_file_data: BinaryIO
    ) -> list[IngestedDoc]:
        logger.debug(f"Ingesting binary data with file_name={file_name}")
        file_data = raw_file_data.read()
        return self._ingest_data(file_name, file_data)

    def bulk_ingest(self, files: list[tuple[str, Path]]) -> list[IngestedDoc]:
        logger.info(f"Ingesting file_names={[f[0] for f in files]}")
        documents = self.ingest_component.bulk_ingest(files)
        logger.info(f"Finished ingestion file_name={[f[0] for f in files]}")
        return [IngestedDoc.from_document(document) for document in documents]

    def list_ingested(self) -> list[IngestedDoc]:
        ingested_docs = []
        try:
            docstore = self.storage_context.docstore
            ingested_docs_ids: set[str] = set()

            for node in docstore.docs.values():
                if node.ref_doc_id is not None:
                    ingested_docs_ids.add(node.ref_doc_id)

            for doc_id in ingested_docs_ids:
                ref_doc_info = docstore.get_ref_doc_info(ref_doc_id=doc_id)
                doc_metadata = None
                if ref_doc_info is not None and ref_doc_info.metadata is not None:
                    doc_metadata = IngestedDoc.curate_metadata(ref_doc_info.metadata)
                ingested_docs.append(
                    IngestedDoc(
                        object="ingest.document",
                        doc_id=doc_id,
                        doc_metadata=doc_metadata,
                    )
                )
        except ValueError:
            logger.warning("Got an exception when getting list of docs", exc_info=True)
            pass
        logger.debug(f"Found count={len(ingested_docs)} ingested documents")
        return ingested_docs

    def delete(self, doc_id: str) -> None:
        """Delete an ingested document.

        :raises ValueError: if the document does not exist
        """
        logger.info(
            "Deleting the ingested document=%s in the doc and index store", doc_id
        )
        self.ingest_component.delete(doc_id)
