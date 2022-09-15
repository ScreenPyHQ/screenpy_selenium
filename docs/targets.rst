=======
Targets
=======

The blocking of the screenplay!
The Target tells the Actors
what part of the website
they are to interact with.

Stripping away the metaphor,
the :ref:`target` combines a locator
with a human-readable string.
The human-readable part
is what gets read out
during :external+screenpy:ref:`Narration`,
and what any :external+screenpy:ref:`exceptions` will use
in their messages.

For example,
we might have some Targets
describing a login page::

    # example_test/ui/login_page.py

    from screenpy_selenium import Target

    USERNAME_FIELD = Target.the("username field").located_by("#username")
    PASSWORD_FIELD = Target.the("password field").located_by("#password")
    SIGN_IN_BUTTON = Target.the('"Sign In" button').located_by("input[type=submit]")

These three Targets
can then be used in our tests
by passing them to Actions::

    # example_test/features/test_login.py

    from screenpy import AnActor
    from screenpy.actions import Eventually
    from screenpy_selenium.abilities import BrowseTheWeb
    from screenpy_selenium.actions import Click, Enter

    from example_test.ui.login_page import (
        PASSWORD_FIELD,
        SIGN_IN_BUTTON
        USERNAME_FIELD,
    )


    Webster = AnActor.named("Webster").who_can(BrowseTheWeb.using_firefox())

    Webster.attempts_to(
        Eventually(Enter.the_text("webster_1987").into_the(USERNAME_FIELD)),
        Enter.the_secret("reallySecurePassword!!").into_the(PASSWORD_FIELD),
        Click.on_the(SIGN_IN_BUTTON),
    )

The resulting log::

    Webster enters "webster_1987" into the username field.
    Webster enters "[CENSORED]" into the password field.
    Websert clicks on the "Sign In" button.

By default the :ref:`target` will use the locator string as a human-readable
target name in the absense of providing one. This can be convenient if your
locators are self-describing::

    from screenpy_selenium import Target
    from selenium.webdriver.common.by import By
    
    USERNAME_FIELD = Target().located((By.ID, "username-field"))
    PASSWORD_FIELD = Target().located((By.ID, "password-field"))
    SIGN_IN_BUTTON = Target().located((By.ID, "sign-in-button"))
    
    Webster.attempts_to(
        Enter.the_text("foo").into_the(USERNAME_FIELD),
        Enter.the_secret("bar").into_the(PASSWORD_FIELD),
        Click.on_the(SIGN_IN_BUTTON),
    )

The resulting log::

    Webster enters "foo" into the username-field.
    Webster enters "[CENSORED]" into the password-field.
    Websert clicks on the sign-in-button.

