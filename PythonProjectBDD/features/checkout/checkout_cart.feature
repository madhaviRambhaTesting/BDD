# MDP-310 – Cart Management (SauceDemo / PayStream Q2 F2 Standard Checkout)
# Mapped from: MDP-9  [PayStream Q2] EPIC: Functional and Integration Testing
#              MDP-14 [PayStream Q2] Functional & Regression Testing Execution
#
# Acceptance Criteria:
#   AC-CART-1  Logged-in user can add one or more items to the cart; badge count updates.
#   AC-CART-2  User can remove individual items from the cart; badge count decrements.
#   AC-CART-3  When the LAST item is removed the UI displays data-testid="empty-cart-banner".
#   AC-CART-4  Clicking Checkout with items navigates to the Checkout: Your Information page.
#   AC-CART-5  locked_out_user is blocked at login and cannot reach the cart.
#   AC-CART-6  problem_user experiences degraded-but-non-fatal cart behaviour (boundary row).

Feature: Checkout Cart Management
  As a logged-in shopper
  I want to add and remove items from my cart
  So that I can control my order before proceeding to checkout

  Background:
    Given I am logged in as "standard_user"

  # ── Positive flows ──────────────────────────────────────────────
  @smoke @checkout @MDP-310
  Scenario: Add a single item and proceed to checkout
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"
    When I navigate to the cart
    Then I should see "Sauce Labs Backpack" in the cart
    When I click "Checkout"
    Then I should be on the "Checkout: Your Information" page

  @regression @checkout @MDP-310
  Scenario: Add multiple items and verify badge count
    When I add "Sauce Labs Backpack" to the cart
    And  I add "Sauce Labs Bike Light" to the cart
    Then the cart badge should show "2"
    When I navigate to the cart
    Then I should see "Sauce Labs Backpack" in the cart
    And  I should see "Sauce Labs Bike Light" in the cart

  @regression @checkout @MDP-310
  Scenario: Remove one item from a multi-item cart
    When I add "Sauce Labs Backpack" to the cart
    And  I add "Sauce Labs Bike Light" to the cart
    And  I navigate to the cart
    And  I remove "Sauce Labs Bike Light" from the cart
    Then the cart badge should show "1"
    And  I should not see "Sauce Labs Bike Light" in the cart

  # ── Negative / empty-cart flows ──────────────────────────────────
  @regression @checkout @MDP-310
  Scenario: Removing the last item displays the empty-cart banner
    When I add "Sauce Labs Backpack" to the cart
    And  I navigate to the cart
    And  I remove "Sauce Labs Backpack" from the cart
    Then the empty-cart banner should be visible

  @regression @checkout @MDP-310
  Scenario: Clicking Checkout on an empty cart displays the empty-cart banner
    When I navigate to the cart
    And  I click "Checkout"
    Then the empty-cart banner should be visible

  # ── Boundary / persona outline ───────────────────────────────────
  @regression @checkout @MDP-310
  Scenario Outline: Add every product to the cart for different user personas
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
