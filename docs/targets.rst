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
by the :external+screenpy:ref:`narrator`,
and what the :external+screenpy:ref:`exceptions` will use
in their messages.

For example,
we might have some Targets
describing a login page::

    from screenpy_selenium import Target

    USERNAME_FIELD = Target.the("username field").located_by("#username")
    PASSWORD_FIELD = Target.the("password field").located_by("#password")
    SIGN_IN_BUTTON = Target.the('"Sign In" button').located_by("input[type=submit]")

These three Targets
can then be used in our tests
by passing them to Actions::

    from screenpy import AnActor
    from screenpy_selenium.abilities import BrowseTheWeb
    from screenpy_selenium.actions import Click, Enter, Eventually

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
