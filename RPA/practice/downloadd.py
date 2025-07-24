from RPA.Robocorp.Process import Process
from RPA.HTTP import HTTP
import os

def download_artifacts_matching(self,filematch=".xlsx"):
    work_items = Process.list_process_work_items()
    for item in work_items:
        artifacts = Process.list_run_artifacts(
            process_run_id=item["processRunId"],
            step_run_id=item["activityRunId"]
        )
        for artifact in artifacts:
            if filematch in artifact["fileName"]:
                download_link = Process.get_robot_run_artifact(
                    process_run_id=item["processRunId"],
                    step_run_id=item["activityRunId"],
                    artifact_id=artifact["id"],
                    filename=artifact["fileName"]
                )
                target_filepath = os.path.join(
                    os.getenv("ROBOT_ARTIFACTS"),
                    f"{artifact['fileName']}"
                )
                HTTP().download(
                    url=download_link,
                    target_file=target_filepath,
                    overwrite=True,
                    stream=True
                )
                
download_artifacts_matching("exe.xlsx")