# PAYSTRM-201 – Add Items to Cart & Proceed to Checkout
# Covers: positive flow, negative/empty-cart guard, boundary (max quantity), edge cases

Feature: Checkout Cart Management
  As a logged-in shopper
  I want to add items to my cart and proceed to checkout
  So that I can purchase products successfully

  Background:
    Given I am logged in as a standard user

  # ── Positive flows ──────────────────────────────────────────────
  @smoke @checkout @PAYSTRM-201
  Scenario: Successfully add a single item to the cart and proceed to checkout
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"
    When I navigate to the cart
    Then I should see "Sauce Labs Backpack" in the cart
    When I click "Checkout"
    Then I should be on the "Checkout: Your Information" page

  @regression @checkout @PAYSTRM-201
  Scenario: Successfully add multiple items to the cart
    When I add "Sauce Labs Backpack" to the cart
    And  I add "Sauce Labs Bike Light" to the cart
    Then the cart badge should show "2"
    When I navigate to the cart
    Then I should see "Sauce Labs Backpack" in the cart
    And  I should see "Sauce Labs Bike Light" in the cart

  @regression @checkout @PAYSTRM-201
  Scenario: Remove an item from the cart before checkout
    When I add "Sauce Labs Backpack" to the cart
    And  I add "Sauce Labs Bike Light" to the cart
    And  I navigate to the cart
    And  I remove "Sauce Labs Bike Light" from the cart
    Then the cart badge should show "1"
    And  I should not see "Sauce Labs Bike Light" in the cart

  # ── Negative flows ───────────────────────────────────────────────
  @regression @checkout @PAYSTRM-201
  Scenario: Attempting checkout with an empty cart shows a warning
    When I navigate to the cart
    And  I click "Checkout"
    Then I should see the message "Your cart is empty"

  # ── Boundary / Edge cases ────────────────────────────────────────
  @regression @checkout @PAYSTRM-201
  Scenario Outline: Add every available product to the cart individually
    When I add "<product>" to the cart
    Then the cart badge should show "<expected_count>"

    Examples:
      | product                       | expected_count |
      | Sauce Labs Backpack           | 1              |
      | Sauce Labs Bike Light         | 1              |
      | Sauce Labs Bolt T-Shirt       | 1              |
      | Sauce Labs Fleece Jacket      | 1              |
      | Sauce Labs Onesie             | 1              |
      | Test.allTheThings() T-Shirt   | 1              |
