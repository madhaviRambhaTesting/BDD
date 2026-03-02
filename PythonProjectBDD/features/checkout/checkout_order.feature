# MDP-312 – Checkout Order Completion (SauceDemo / PayStream Q2 F1/F2 Checkout Flows)
# Mapped from: MDP-9  [PayStream Q2] EPIC: Functional and Integration Testing
#              MDP-14 [PayStream Q2] Functional & Regression Testing Execution
#
# Acceptance Criteria:
#   AC-ORD-1  Valid first name, last name, and postal code advance the user to Overview.
#   AC-ORD-2  Missing first name  → inline error "Error: First Name is required".
#   AC-ORD-3  Missing last name   → inline error "Error: Last Name is required".
#   AC-ORD-4  Missing postal code → inline error "Error: Postal Code is required".
#   AC-ORD-5  Overview shows item subtotal = sum of item prices; total = subtotal + tax.
#   AC-ORD-6  Finish navigates to Checkout: Complete! with "Thank you for your order!".
#   AC-ORD-7  Cancel on info page returns user to cart with items intact.
#   AC-ORD-8  locked_out_user cannot reach checkout (blocked at login — see persona outline).
#   AC-ORD-9  problem_user boundary inputs must behave identically to standard_user.

Feature: Checkout Order Completion
  As a logged-in shopper
  I want to provide shipping information and confirm my order
  So that I receive an order confirmation

  Background:
    Given I am logged in as "standard_user"
    And   I have "Sauce Labs Backpack" in my cart
    And   I am on the "Checkout: Your Information" page

  # ── Positive flows ──────────────────────────────────────────────
  @smoke @checkout @MDP-312
  Scenario: Complete a checkout with valid shipping details
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should be on the "Checkout: Overview" page
    And  I should see "Sauce Labs Backpack" in the order summary
    When I click "Finish"
    Then I should be on the "Checkout: Complete!" page
    And  I should see the message "Thank you for your order!"

  @regression @checkout @MDP-312
  Scenario: Order overview shows correct price totals
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then the item total should match the sum of all item prices
    And  the tax amount should be displayed
    And  the order total should equal item total plus tax

  # ── Negative / validation flows ───────────────────────────────────
  @regression @checkout @MDP-312
  Scenario: Checkout blocked when First Name is missing
    When I leave the first name blank
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should see the error message "Error: First Name is required"

  @regression @checkout @MDP-312
  Scenario: Checkout blocked when Last Name is missing
    When I enter first name "Jane"
    And  I leave the last name blank
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should see the error message "Error: Last Name is required"

  @regression @checkout @MDP-312
  Scenario: Checkout blocked when Postal Code is missing
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I leave the postal code blank
    And  I click "Continue"
    Then I should see the error message "Error: Postal Code is required"

  @regression @checkout @MDP-312
  Scenario: Cancel on checkout info page returns user to cart
    When I click "Cancel"
    Then I should be on the "Your Cart" page
    And  I should see "Sauce Labs Backpack" in the cart

  # ── Boundary / persona outline ────────────────────────────────────
  @regression @checkout @MDP-312
  Scenario Outline: Checkout form validates boundary inputs across personas
    Given I am logged in as "<persona>"
    And   I have "Sauce Labs Backpack" in my cart
    And   I am on the "Checkout: Your Information" page
    When I enter first name "<first_name>"
    And  I enter last name "<last_name>"
    And  I enter postal code "<postal_code>"
    And  I click "Continue"
    Then I should see the result "<expected_result>"

    Examples:
      | persona         | first_name | last_name | postal_code | expected_result                 |
      | standard_user   | A          | B         | 1           | Checkout: Overview              |
      | standard_user   | Jane       | Doe       | 00000       | Checkout: Overview              |
      | standard_user   |            | Doe       | 90210       | Error: First Name is required   |
      | standard_user   | Jane       |           | 90210       | Error: Last Name is required    |
      | standard_user   | Jane       | Doe       |             | Error: Postal Code is required  |
      | problem_user    | Jane       | Doe       | 90210       | Checkout: Overview              |
      | problem_user    |            | Doe       | 90210       | Error: First Name is required   |
      | locked_out_user | Jane       | Doe       | 90210       | locked_out                      |
