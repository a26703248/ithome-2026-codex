# Repository instructions

## Scope
- These instructions apply to every file under this directory.

## Project
- Use Java 17 and Maven.
- Production code is under `src/main/java`; tests are under `src/test/java`.

## Change boundaries
- For bug fixes, do not rewrite existing tests or edit `pom.xml` unless the task explicitly allows it.
- Ask before adding dependencies, deleting files, or changing public APIs.

## Verification
- Run the smallest relevant test first, then run `mvn clean test` after changing Java code.
- If a command cannot run, report the exact error and do not claim tests passed.

## Completion report
- List changed files, commands run, test results, and remaining risks.
