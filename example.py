from filter import Pipeline, Filter, Operation, Clause, AND, OR, Option


def main():
    Pipeline([
        Filter(
            "Ignore",
            Operation(OR, [
                Operation(AND, [
                    Clause("from:noreply@md.getsentry.com"),
                    Clause("subject:\"Advertisement\""),
                    Clause("subject:\"False Alarm\""),
                ]),
                Operation(OR, [
                    Clause("from:sam@example.com"),
                    Clause("cc:jiwon@example.com"),
                ]),
                Clause("from:noreply@lokalise.com"),
                Clause("to:cream@example.com"),
            ]),
            Option(apply_label=False, skip_inbox=True),
        ),
        Filter(
            "Alarm",
            Operation(OR, [
                Operation(AND, [
                    Clause("to:alarm@example.com"),
                    Clause("subject:ALARM"),
                ]),
                Operation(AND, [
                    Clause("from:alert@dtdg.co"),
                    Clause("to:monitor@md.getsentry.com"),
                ]),
                Clause("from:noreply@md.getsentry.com"),
            ]),
        ),
        Filter(
            "Report",
            Operation(OR, [
                Clause("subject:\"News\""),
                Clause("subject:\"Weekly Report\""),
                Clause("to:collector@example.com"),
            ]),
        ),
        Filter(
            "SE/Game",
            Clause("to:engineer+game@example.com"),
        ),
        Filter(
            "SE",
            Operation(OR, [
                Clause("to:engineer@example.com"),
                Clause("to:request@example.com"),
            ]),
        ),
        Filter(
            "example",
            Clause("from:@example.com"),
        ),
    ]).save("output.xml")


main()

