# onedrive-pipe-poc

## Prerequisites

### Accounts

- Power Automate Premium
- OneDrive
- [ngrok](https://ngrok.com)

> [!NOTE]
> Power Automate requires a business account and at least a Premium-tier
> subscription. Your Power Automate and OneDrive accounts do not need to be
> under the same email, so you can use your personal OneDrive, but you need an
> organizational email for Power Automate.

### Tech Stack

- [mise](https://mise.jdx.dev)
- Docker

## Local Development

### ngrok Setup

1. Create a free ngrok account.
2. From the dashboard, you can get your free domain and auth token.

### Webhook Server Setup

1. Clone this repo.
2. Install dependencies:

    ```shell
    mise trust -y
    mise install -y
    uv sync
    ```

3. Copy `.env.example` into a new `.env` file and provide the appropriate values.
4. Run the ngrok tunnel:

    ```shell
    docker compose up
    ```

5. In a separate terminal, run the webhook server:

    ```shell
    uv run -- fastapi dev
    ```

### OneDrive & Power Automate Setup

1. Create/upload an Excel file containing tabular data to your OneDrive.
2. In the Power Automate dashboard, navigate to **Connections** and connect your
   OneDrive account.
3. Navigate to **Create** and create an **Automated cloud flow**.
4. Create the following steps:

   1. For the trigger, select *When a file is modified (properties only)*. Add the
      following configuration parameters:
      - **Parameters**
        - **Folder**: the folder containing the Excel file
        - **Include subfolders**: No
        - **Number of files to return**: 1
        - everything else at defaults
   2. *Get file content*
      - **Parameters**
        - **File**: the exact file path
        - **Infer Content Type**: Yes
   3. *HTTP Webhook*
      - **Parameters**
        - **Subscribe Method**: POST
        - **Subscribe URI**: `https://your_free_ngrok.domain/api/webhook`
        - **Subscribe Body**: File content
        - **Advanced parameters**: Subscribe Headers
        - **Subscribe Headers**:
          - | Authorization | Bearer your_WEBHOOK_SECRET_from_.env |
          - | Content-Type | application/octet-stream |

   > [!INFO]
   > **HTTP Webhook** is a "premium" step, which is why a Premium account is needed.

5. Save and turn on the automation.
6. To test, edit the file in OneDrive. You should see some terminal logs shortly.
   Excel and Parquet files should be written in [app/uploads](./app/uploads/).
