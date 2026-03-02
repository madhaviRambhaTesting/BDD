# ══════════════════════════════════════════════════════════════════════════════
# Feature  : Checkout Cart Management
# Stories  : MDP-9  – [PayStream Q2] EPIC: Functional and Integration Testing
#            MDP-14 – [PayStream Q2] Functional & Regression Testing Execution
# Framework: pytest-bdd + Selenium (headless Chrome)
# Branch   : feature/bdd-checkout
# ──────────────────────────────────────────────────────────────────────────────
# Acceptance Criteria
# ───────────────────
#   AC-CART-1  Logged-in user can add one or more items to the cart; badge updates.
#   AC-CART-2  User can remove individual items; badge count decrements correctly.
#   AC-CART-3  When the LAST item is removed the UI displays the element
#              with data-test="cart-empty-banner" (confirmed AUT selector).
#   AC-CART-4  Clicking Checkout with items navigates to "Checkout: Your Information".
#   AC-CART-5  problem_user experiences degraded-but-non-fatal behaviour;
#              add-to-cart still works and badge reaches 1.
#   AC-CART-6  locked_out_user is covered as a dedicated @xfail scenario
#              in checkout_order.feature (not in this cart outline).
#
# Test types: smoke · regression · boundary
# ══════════════════════════════════════════════════════════════════════════════

Feature: Checkout Cart Management
  As a logged-in shopper on the SauceDemo storefront
  I want to add and remove items from my shopping cart
  So that I can review and control my order before proceeding to checkout

  Background:
    Given I am logged in as "standard_user"

  # ── Positive flows ──────────────────────────────────────────────────────────

  @smoke @checkout @MDP-9 @MDP-14
  Scenario: Add a single item and proceed to checkout
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"
    When I navigate to the cart
    Then I should see "Sauce Labs Backpack" in the cart
    When I click "Checkout"
    Then I should be on the "Checkout: Your Information" page

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Add multiple items and verify badge count
    When I add "Sauce Labs Backpack" to the cart
    And  I add "Sauce Labs Bike Light" to the cart
    Then the cart badge should show "2"
    When I navigate to the cart
    Then I should see "Sauce Labs Backpack" in the cart
    And  I should see "Sauce Labs Bike Light" in the cart

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Remove one item from a multi-item cart leaves remaining item
    When I add "Sauce Labs Backpack" to the cart
    And  I add "Sauce Labs Bike Light" to the cart
    And  I navigate to the cart
    And  I remove "Sauce Labs Bike Light" from the cart
    Then the cart badge should show "1"
    And  I should not see "Sauce Labs Bike Light" in the cart

  # ── Negative / empty-cart flows (AC-CART-3) ────────────────────────────────

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Removing the last item displays the empty-cart banner
    # AC-CART-3: AUT must render data-test="cart-empty-banner" after last removal
    When I add "Sauce Labs Backpack" to the cart
    And  I navigate to the cart
    And  I remove "Sauce Labs Backpack" from the cart
    Then the empty-cart banner should be visible

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Clicking Checkout on an empty cart displays the empty-cart banner
    # AC-CART-3: empty cart guard must prevent navigation and show the banner
    When I navigate to the cart
    And  I click "Checkout"
    Then the empty-cart banner should be visible

  # ── Boundary / persona outline (AC-CART-5) ─────────────────────────────────
  # locked_out_user intentionally excluded from this outline.
  # See checkout_order.feature for the dedicated @xfail locked_out scenario.

  @regression @checkout @MDP-9 @MDP-14
  Scenario Outline: Add every SauceDemo product across user personas
    Given I am logged in as "<persona>"
    When I add "<product>" to the cart
    Then the cart outcome should be "<expected_outcome>"

    Examples:
      | persona       | product                     | expected_outcome |
      | standard_user | Sauce Labs Backpack         | badge:1          |
      | standard_user | Sauce Labs Bike Light       | badge:1          |
      | standard_user | Sauce Labs Bolt T-Shirt     | badge:1          |
      | standard_user | Sauce Labs Fleece Jacket    | badge:1          |
      | standard_user | Sauce Labs Onesie           | badge:1          |
      | standard_user | Test.allTheThings() T-Shirt | badge:1          |
      | problem_user  | Sauce Labs Backpack         | badge:1          |
      | problem_user  | Sauce Labs Bike Light       | badge:1          |
