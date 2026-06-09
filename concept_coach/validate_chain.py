from build_chain import build_chain


def is_response_valid(response: str) -> tuple[bool, list[str]]:
    errors = []

    if not isinstance(response, str):
        errors.append("Response must be a string.")
        return False, errors

    if not response.strip():
        errors.append("Response must not be empty after trimming spaces.")

    if len(response.split()) > 100:
        errors.append("Response must not be more than 100 words.")

    return len(errors) == 0, errors


def main():
    chain = build_chain()

    test_cases = [
        {
            "topic": "LangChain Expression Language",
            "analogy_domain": "school assembly line",
        },
        {
            "topic": "Prompt Templates",
            "analogy_domain": "wedding invitation cards",
        },
        {
            "topic": "Output Parsers",
            "analogy_domain": "food delivery packaging",
        },
    ]

    for i, test_input in enumerate(test_cases, start=1):
        print(f"\n{'=' * 50}")
        print(f"Test Case {i}")
        print(f"{'=' * 50}")

        response = chain.invoke(test_input)

        is_valid, errors = is_response_valid(response)

        print("Input Dictionary:")
        print(test_input)

        print("\nGenerated Response:")
        print(response)

        print("\nValidation Result:")
        print(is_valid)

        if errors:
            print("\nValidation Errors:")
            for error in errors:
                print(f"- {error}")


if __name__ == "__main__":
    main()