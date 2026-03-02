# ══════════════════════════════════════════════════════════════════════════════
# Feature  : Checkout Order Completion
# Stories  : MDP-9  – [PayStream Q2] EPIC: Functional and Integration Testing
#            MDP-14 – [PayStream Q2] Functional & Regression Testing Execution
# Framework: pytest-bdd + Selenium (headless Chrome)
# Branch   : feature/bdd-checkout
# ──────────────────────────────────────────────────────────────────────────────
# Acceptance Criteria
# ───────────────────
#   AC-ORD-1  Valid first name, last name, and postal code advance to Overview.
#   AC-ORD-2  Missing first name  → inline error "Error: First Name is required".
#   AC-ORD-3  Missing last name   → inline error "Error: Last Name is required".
#   AC-ORD-4  Missing postal code → inline error "Error: Postal Code is required".
#   AC-ORD-5  Overview shows item subtotal = sum of item prices;
#             order total = subtotal + tax (BR-PRICE).
#   AC-ORD-6  Clicking Finish navigates to "Checkout: Complete!" with
#             "Thank you for your order!" confirmation header.
#   AC-ORD-7  Clicking Cancel on the info page returns the user to the cart
#             with all items still present.
#   AC-ORD-8  problem_user boundary inputs behave identically to standard_user.
#   AC-ORD-9  locked_out_user is blocked at login and never reaches checkout
#             — covered as a standalone @xfail scenario (not an outline row).
#
# Test types: smoke · regression · boundary · xfail
# ══════════════════════════════════════════════════════════════════════════════

Feature: Checkout Order Completion
  As a logged-in shopper on the SauceDemo storefront
  I want to provide shipping information and confirm my order
  So that I receive an order confirmation and the order is placed

  Background:
    Given I am logged in as "standard_user"
    And   I have "Sauce Labs Backpack" in my cart
    And   I am on the "Checkout: Your Information" page

  # ── Positive flows ──────────────────────────────────────────────────────────

  @smoke @checkout @MDP-9 @MDP-14
  Scenario: Complete a checkout with valid shipping details (AC-ORD-1, AC-ORD-6)
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should be on the "Checkout: Overview" page
    And  I should see "Sauce Labs Backpack" in the order summary
    When I click "Finish"
    Then I should be on the "Checkout: Complete!" page
    And  I should see the message "Thank you for your order!"

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Order overview shows correct price totals (AC-ORD-5 / BR-PRICE)
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should be on the "Checkout: Overview" page
    And  the item total should match the sum of all item prices
    And  the tax amount should be displayed
    And  the order total should equal item total plus tax

  # ── Negative / validation flows (AC-ORD-2, AC-ORD-3, AC-ORD-4) ────────────

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Checkout blocked when First Name is missing (AC-ORD-2)
    When I leave the first name blank
    And  I enter last name "Doe"
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should see the error message "Error: First Name is required"

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Checkout blocked when Last Name is missing (AC-ORD-3)
    When I enter first name "Jane"
    And  I leave the last name blank
    And  I enter postal code "90210"
    And  I click "Continue"
    Then I should see the error message "Error: Last Name is required"

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Checkout blocked when Postal Code is missing (AC-ORD-4)
    When I enter first name "Jane"
    And  I enter last name "Doe"
    And  I leave the postal code blank
    And  I click "Continue"
    Then I should see the error message "Error: Postal Code is required"

  # ── Edge / cancel flow (AC-ORD-7) ──────────────────────────────────────────

  @regression @checkout @MDP-9 @MDP-14
  Scenario: Cancel on checkout info page returns user to cart with items intact (AC-ORD-7)
    When I click "Cancel"
    Then I should be on the "Your Cart" page
    And  I should see "Sauce Labs Backpack" in the cart

  # ── Boundary / persona outline (AC-ORD-1, AC-ORD-2, AC-ORD-3, AC-ORD-8) ───
  # locked_out_user is NOT in this outline — see the dedicated @xfail below.

  @regression @checkout @MDP-9 @MDP-14
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
      | persona       | first_name | last_name | postal_code | expected_result                |
      | standard_user | A          | B         | 1           | Checkout: Overview             |
      | standard_user | Jane       | Doe       | 00000       | Checkout: Overview             |
      | standard_user |            | Doe       | 90210       | Error: First Name is required  |
      | standard_user | Jane       |           | 90210       | Error: Last Name is required   |
      | standard_user | Jane       | Doe       |             | Error: Postal Code is required |
      | problem_user  | Jane       | Doe       | 90210       | Checkout: Overview             |
      | problem_user  |            | Doe       | 90210       | Error: First Name is required  |

  # ── locked_out_user – dedicated @xfail scenario (AC-ORD-9) ─────────────────
  # Reason: locked_out_user is always blocked at login; marking as xfail
  # documents the known constraint without poisoning outline results.
  # When the persona is unblocked (e.g. test-env toggle), promote to @xpass.

  @regression @checkout @MDP-9 @MDP-14 @xfail
  Scenario: locked_out_user is blocked at login and cannot reach checkout (AC-ORD-9)
    # Override Background: log in explicitly as locked_out_user
    Given I am logged in as "locked_out_user"
    Then I should see the login error banner
