from app.agents.sheet_agent import SheetAgent


SHEET_NAME = "Youtube_Automation"


def main():

    agent = SheetAgent()

    agent.execute(
        SHEET_NAME,
    )


if __name__ == "__main__":
    main()