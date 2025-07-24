from RPA.Robocorp.Process import Process
from RPA.Robocorp.Vault import Vault

secrets = Vault().get_secret("ProcessAPI")
process = Process(
    secrets["workspace_id"],
    secrets["process_id"],
    secrets["apikey"]
)


def retry_failed_items():
    items = process.list_process_work_items()
    for item in items:
        if item["state"] == "FAILED":
            print("FAILED work item: %s" % item["id"])
            result = process.retry_work_item(item["id"])
            print(result)

if __name__ == "__main__":
    retry_failed_items()