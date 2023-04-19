.. _cookbook:

=========================
ScreenPy Selenium Recipes
=========================

This collection contains
examples of common ScreenPy Selenium use-cases.
For other recipes of interest,
see ScreenPy's :external+screenpy:ref:`screenpy recipes`.


.. _actor_setup:

Setting Up Actors
=================

Set up an Actor to browse the web::

    Perry = AnActor.who_can(BrowseTheWeb.using_firefox())

Set up an Actor to browse the web with a specific driver::

    options = webdriver.ChromeOptions()
    options.set_headless()
    # ... other setup, maybe
    driver = webdriver.Chrome(options=options)

    Perry = AnActor.who_can(BrowseTheWeb.using(driver))


Attach Debug Information at the End of Tests
============================================

You can tell your Actors to take a screenshot
just before the test is over.

Using ``pytest``
----------------

Creating your Actors as `pytest fixtures <https://docs.pytest.org/en/7.1.x/how-to/fixtures.html>`__
allows you to easily take screenshots and save the console log
after the test is over::

    from datetime import datetime

    import pytest
    from screenpy import AnActor
    from screenpy_selenium import BrowseTheWeb, SaveConsoleLog, SaveScreenshot


    @pytest.fixture()
    def Sammy():
        # arrange
        the_actor = AnActor.named("Sammy").who_can(BrowseTheWeb.using_firefox())

        # act
        yield the_actor  # assert happens somewhere in here, probably

        # cleanup
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")
        file_prefix = f"{DEBUG_DIR_PATH}/{timestamp}_sammy_endtest"
        the_actor.attempts_to(
            SaveScreenshot.as_(f"{file_prefix}_screenshot.png").and_attach_it(),
            SaveConsoleLog.as_(f"{file_prefix}_js_log.txt").and_attach_it(),
        )
        the_actor.exit()

If you only want this information when a test fails,
you can tweak this fixture using the information
from `pytest's examples <https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures>`__.


Using ``unittest.TestCase``
---------------------------

During the teardown steps of your test,
you can use your Actor to take screenshots
before exiting::

    from datetime import datetime

    import unittest
    from screenpy import AnActor
    from screenpy_selenium import BrowseTheWeb, SaveConsoleLog, SaveScreenshot


    class TestSomething(unittest.TestCase):

        def setUp(self):
            self.actor = AnActor.named("Sammy").who_can(BrowseTheWeb.using_firefox())

        def test_the_thing(self):
            Sammy = self.actor
            ...

        def tearDown(self):
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")
            file_prefix = f"{DEBUG_DIR_PATH}/{timestamp}_sammy_endtest"
            self.actor.attempts_to(
                SaveScreenshot.as_(f"{file_prefix}_screenshot.png").and_attach_it(),
                SaveConsoleLog.as_(f"{file_prefix}_js_log.txt").and_attach_it(),
            )
            self.actor.exit()

If you only want this information when a test fails,
you can tweak this code following
`this StackOverflow answer <https://stackoverflow.com/a/39606065>`__
(sorry there isn't a better source!).


Waiting
=======

Automated tests go *fast*.
You will probably need to wait for your pages
to be ready for your Actions.
Here are some strategies you can use.

Using Wait
----------

:class:`~screenpy_selenium.actions.Wait` tells the Actor to stop until some condition is met.
Here are some examples of its use.

Bread-and-butter default wait,
waits 20 seconds for the login modal to appear::

    Perry.attempts_to(Wait.for_the(LOGIN_MODAL))


Wait for a non-default timeout
and a different condition::

    Perry.attempts_to(Wait(42).seconds_for(THE_WELCOME_BANNER).to_disappear())


Using a custom condition,
wait 20 seconds
for the application to meet the condition::

    class appear_in_greyscale:
        def __init__(self, locator):
            self.locator = locator

        def __call__(self, driver):
            element = driver.find_element(*self.locator)
            return element.value_of_css_property("filter") == "grayscale(100%)"

    Perry.attempts_to(Wait.for_the(PROFILE_ICON).to(appear_in_greyscale))


Using a custom condition
which does not use a Target::

    def url_minimum_length_with_text(length, text):
        def _predicate(driver):
            return text in driver.url and len(driver.url) >= length

        return _predicate

    Perry.attempts_to(
        #   ⇩ note the parentheses here
        Wait().using(url_minimum_length_with_text).with_(20, "hello")
    )


Using Eventually
----------------

The :external+screenpy:class:`~screenpy.actions.Eventually` Action
deserves a special mention in this section.

:external+screenpy:class:`~screenpy.actions.Eventually` can take the place
of :class:`~screenpy_selenium.actions.Wait`,
if you're only waiting
for an element to appear
or to be clickable.
This can reduce the length of your tests
while still being quite readable
and robust.

Here's a quick before/after example::

    # ⇩ before

    when(Brody).attempts_to(
        Wait.for_the(REGISTER_LINK).to_be_clickable(),
        Click.on_the(REGISTER_LINK),
        Wait.for_the(NICKNAME_FIELD).to_appear(),
        Enter.the_text("Brody").into_the(NICKNAME_FIELD)),
        Enter.the_text("Brodiferous").into_the(FULL_NAME_FIELD),
        Click.on_the(SUBMIT_BUTTON),
        Wait.for_the(WELCOME_BANNER).to_appear(),
    )

    then(Brody).should(
        See.the(Text.of_the(WELCOME_BANNER), ContainsTheText("Brody")),
    )

.. code-block:: python

    # ⇩ after

    when(Brody).attempts_to(
        Eventually(Click.on_the(REGISTER_LINK)),
        Eventually(Enter.the_text("Brody").into_the(NICKNAME_FIELD)),
        Enter.the_text("Brodiferous").into_the(FULL_NAME_FIELD),
        Click.on_the(SUBMIT_BUTTON),
    )

    then(Brody).should(
        Eventually(
            See.the(Text.of_the(WELCOME_BANNER), ContainsTheText("Brody"))
        ),
    )

See the entry in the
:external+screenpy:ref:`ScreenPy Cookbook <the eventually class>`
for more information on using this class.
