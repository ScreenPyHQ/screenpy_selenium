.. _cookbook:

=========================
ScreenPy+Selenium Recipes
=========================

This collection contains
examples of common ScreenPy+Selenium use-cases.
For other recipes of interest,
see ScreenPy's :external+screenpy:ref:`cookbook`.


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


Waiting
=======

Bread-and-butter default wait,
waits 20 seconds for the login modal to appear::

    Perry.attempts_to(Wait.for_the(LOGIN_MODAL))


Wait for a non-default timeout
and a different condition::

    Perry.attempts_to(Wait(42).seconds_for(THE_WELCOME_BANNER).to_disappear())


Using a custom condition,
wait 20 seconds
for the application
to meet the condition::

    class appear_in_greyscale:
        def __init__(self, locator):
            self.locator = locator

        def __call__(self, driver):
            element = driver.find_element(*self.locator)
            return element.value_of_css_property(filter) == "grayscale(100%)"

    Perry.attempts_to(Wait.for_the(PROFILE_ICON).to(appear_in_greyscale))


Using a custom condition
which does not use a Target::

    def url_to_contain_text_and_be_at_least_this_long(text, length):
        def _predicate(driver):
            return text in driver.url and len(driver.url) >= length

        return _predicate

    Perry.attempts_to(
        #   ⇩ note the parentheses here
        Wait().using(
            url_to_contain_text_and_be_at_least_this_long
        ).with_("hello", 20)
    )


The Eventually Class
--------------------

The :external+screenpy:class:`~screenpy.actions.Eventually` Action
deserves a special mention in this section.
See the entry in ScreenPy's :external+screenpy:ref:`cookbook`
for more information on using this class,
but here's a quick example::

    when(Brody).attempts_to(
        Eventually(Click.on_the(REGISTER_LINK)),
        Eventually(Enter.the_text("Brody").into_the(NICKNAME_FIELD)),
        Enter.the_text("Brodiferous").into_the(FULL_NAME_FIELD),
        Click.on_the(SUBMIT_BUTTON),
    )

    then(Brody).should(
        Eventually(See.the(Text.of_the(WELCOME_BANNER), ContainsTheText("Brody"))),
    )
