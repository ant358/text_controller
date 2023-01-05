from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging
import time
from src.input import get_pageids, get_pageids_from_graph, get_title

logger = logging.getLogger(__name__)


# write to the database
def write_document_nodes(pageids: list[str]):
    """
    Write the document nodes to the graph database
    """
    # get the driver
    driver = GraphDatabase.driver("bolt://host.docker.internal:7687")
    try:
        # create the session
        with driver.session() as session:
            # create the nodes
            for pageid in pageids:
                # get the title
                title = get_title(pageid)
                # create the node
                session.run(
                    "MERGE (n:Document {pageId: $pageid, title: $title})",
                    pageid=pageid,
                    title=title)
                # log the creation
                logger.info(f"Created node for {pageid}")
    except ServiceUnavailable:
        logger.error("Neo4j Database unavailable")


def update_document_nodes(status: str, create_doc_nodes):
    """
    Update the document nodes in the graph database

    Args:
        status (str): status of the program
        create_doc_nodes (control.JobList):
            job list for creating document nodes

    Returns:
        None
    """
    while status == 'running':
        # get the pageids
        graph_pageids = get_pageids_from_graph()
        # get the pageids
        source_db_pageids = get_pageids()
        # check if there are any new pageids
        if pageids := [
                pageid for pageid in source_db_pageids
                if pageid not in graph_pageids
        ]:
            # output the pageids to the job list
            create_doc_nodes.bulk_add(pageids)
            # create the pageid nodes
            write_document_nodes(create_doc_nodes.jobs)
        else:
            # log that there are no jobs
            logger.info("No jobs to process")
            # wait for a job to be added
            time.sleep(10)
