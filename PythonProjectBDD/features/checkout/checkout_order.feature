# PAYSTRM-202 – Complete the Checkout Order Flow
# Covers: positive full-flow, field-validation negatives, boundary inputs, order-confirmation edge case

Feature: Checkout Order Completion
  As a logged-in shopper
  I want to fill in shipping details and complete my order
  So that I receive an order confirmation

  Background:
    Given I am logged in as a standard user
    And   I have "Sauce Labs Backpack" in my cart
    And   I am on the "Checkout: Your Information" page

  # ── Positive flows ──────────────────────────────────────────────
  @smoke @checkout @PAYSTRM-202
  Scenario: Successfully complete a checkout with valid details
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should be on the "Checkout: Overview" page
    And  I should see "Sauce Labs Backpack" in the order summary
    When I click "Finish"
    Then I should be on the "Checkout: Complete!" page
    And  I should see the message "Thank you for your order!"

  @regression @checkout @PAYSTRM-202
  Scenario: Order summary shows correct item price and totals
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then the item total should match the sum of all item prices
    And  the tax amount should be displayed
    And  the order total should equal item total plus tax

  # ── Negative flows ───────────────────────────────────────────────
  @regression @checkout @PAYSTRM-202
  Scenario: Checkout fails when First Name is missing
    When I leave the first name blank
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should see the error message "Error: First Name is required"

  @regression @checkout @PAYSTRM-202
  Scenario: Checkout fails when Last Name is missing
    When I enter first name "Jane"
    And  I leave the last name blank
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should see the error message "Error: Last Name is required"

  @regression @checkout @PAYSTRM-202
  Scenario: Checkout fails when Postal Code is missing
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I leave the postal code blank
    And  I click "Continue"
    Then I should see the error message "Error: Postal Code is required"

  # ── Boundary / Edge cases ────────────────────────────────────────
  @regression @checkout @PAYSTRM-202
  Scenario Outline: Checkout form validates boundary inputs
    When I enter first name "<first_name>"
    And  I enter last name "<last_name>"
    And  I enter postal code "<postal_code>"
    And  I click "Continue"
    Then I should see the result "<expected_result>"

    Examples:
      | first_name | last_name | postal_code | expected_result                     |
      | A          | B         | 1           | Checkout: Overview                  |
      | Jane       | Doe       | 00000       | Checkout: Overview                  |
      |            | Doe       | 90210       | Error: First Name is required       |
      | Jane       |           | 90210       | Error: Last Name is required        |
      | Jane       | Doe       |             | Error: Postal Code is required      |

  @regression @checkout @PAYSTRM-202
  Scenario: User can cancel checkout and return to cart
    When I click "Cancel"
    Then I should be on the "Your Cart" page
    And  I should see "Sauce Labs Backpack" in the cart
