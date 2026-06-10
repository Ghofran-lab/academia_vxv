from francaisfacile_scraper.markdown import slugify, to_markdown
from francaisfacile_scraper.parser import discover_exercise_links, parse_exercise


def test_parse_exercise_splits_statement_questions_and_correction():
    html = """
    <html><head><title>Accord du participe passé</title></head>
    <body><nav>menu</nav><main>
      <h1>Accord du participe passé</h1>
      <p>Complétez les phrases suivantes.</p>
      <ol><li>Les pommes que j'ai ____ sont rouges.</li></ol>
      <h2>Correction</h2><p>Les pommes que j'ai mangées sont rouges.</p>
    </main></body></html>
    """

    exercise = parse_exercise(html, "https://www.francaisfacile.com/exercices/exercice-francais-1.php")

    assert exercise.title == "Accord du participe passé"
    assert "Complétez les phrases" in exercise.statement
    assert exercise.questions == ["Les pommes que j'ai ____ sont rouges."]
    assert exercise.correction is not None
    assert "mangées" in exercise.correction


def test_discover_exercise_links_keeps_francaisfacile_exercises_only():
    html = """
    <a href="/exercices/exercice-francais-123.php">ok</a>
    <a href="https://example.com/exercice.php">no</a>
    <a href="/cours/index.php">no</a>
    """

    links = discover_exercise_links(html, "https://www.francaisfacile.com/index.php")

    assert links == ["https://www.francaisfacile.com/exercices/exercice-francais-123.php"]


def test_markdown_contains_front_matter_and_source():
    exercise = parse_exercise(
        "<h1>Les accents français</h1><p>Quel accent manque ?</p>",
        "https://www.francaisfacile.com/exercices/exercice-francais-2.php",
    )

    markdown = to_markdown(exercise)

    assert markdown.startswith("---\ntitle: Les accents français")
    assert "## Source" in markdown
    assert "https://www.francaisfacile.com/exercices/exercice-francais-2.php" in markdown


def test_slugify_removes_accents():
    assert slugify("Les accents français !") == "les-accents-francais"
