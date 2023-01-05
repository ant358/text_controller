# note does not run in jupyter notebook, run in the terminal
from fastapi import FastAPI
import uvicorn
import logging
import os
import pathlib
import time
from datetime import datetime
from src.input_data import get_pageids, get_pageids_from_graph
from src.output_data import write_document_nodes
from src.control import Job_list

# setup logging
# get todays date
datestamp = datetime.now().strftime('%Y%m%d')
container_name = os.getenv('CONTAINER_NAME')
# append date to logfile name
log_name = f'log-{container_name}-{datestamp}.txt'
path = os.path.abspath('./logs/')
# add path to log_name to create a pathlib object
# required for loggin on windows and linux
log_filename = pathlib.Path(path, log_name)

# create log file if it does not exist
if os.path.exists(log_filename) is not True:
    # create the logs folder if it does not exist
    if os.path.exists(path) is not True:
        os.mkdir(path)
    # create the log file
    open(log_filename, 'w').close()

# create logger
logger = logging.getLogger()
# set minimum output level
logger.setLevel(logging.DEBUG)
# Set up the file handler
file_logger = logging.FileHandler(log_filename)

# create console handler and set level to debug
ch = logging.StreamHandler()
# set minimum output level
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('[%(levelname)s] -'
                              ' %(asctime)s - '
                              '%(name)s : %(message)s')
# add formatter
file_logger.setFormatter(formatter)
ch.setFormatter(formatter)
# add a handler to logger
logger.addHandler(file_logger)
logger.addHandler(ch)
# mark the run
logger.info(f'Lets get started! - logginng in "{log_filename}" today')

# create the FastAPI app
app = FastAPI()

# create the job lists
create_doc_nodes = Job_list()
create_ner_nodes = Job_list()

# status
status = "running"


def update_document_nodes(status: str):
    while status == 'running':
        # get the pageids
        graph_pageids = get_pageids_from_graph()
        # get the pageids
        source_db_pageids = get_pageids()
        if pageids := [
                pageid for pageid in source_db_pageids
                if pageid not in graph_pageids
        ]:
            # output the pageids to the job list
            create_doc_nodes.bulk_add(pageids)
            write_document_nodes(create_doc_nodes.jobs)
        else:
            # log that there are no jobs
            logger.info("No jobs to process")
            # wait for a job to be added
            time.sleep(10)


# OUTPUT- routes
@app.get("/")
async def root():
    logging.info("Root requested")
    return {"message": "Text controller API"}


@app.get("/get_current_create_doc_nodes_jobs")
async def get_current_create_doc_nodes_jobs():
    """Get the current create node jobs"""
    logging.info("Current create node jobs list requested")
    return {"Current jobs": create_doc_nodes.jobs}


@app.get("/get_current_create_ner_nodes_jobs")
async def get_current_create_ner_nodes_jobs():
    """Get the current create ner node jobs"""
    logging.info("Current create ner node jobs list requested")
    return {"Current jobs": create_ner_nodes.jobs}


@app.get("/get_status")
async def get_status():
    """Get the status of the controller"""
    logging.info("Status requested")
    return {"Status": status}


# INPUT routes
@app.post("/set_status/{new_status}")
async def set_status(new_status: str):
    """Set the status of the controller"""
    logging.info(f"Status set to {new_status}")
    status = new_status
    return {"Status": status}


if __name__ == "__main__":
    # goto localhost:8080/
    # or localhost:8080/docs for the interactive docs
    uvicorn.run(app, port=8080, host="0.0.0.0")
