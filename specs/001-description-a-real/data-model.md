# Data Model for Real Estate Investment Platform

This document defines the data model for the Real Estate Investment Platform, based on the entities identified in the feature specification.

## User

Represents an individual with an account on the platform.

- **Attributes**:
    - `UserID` (Primary Key)
    - `Name` (String)
    - `Email` (String, Unique)
    - `PasswordHash` (String)
    - `Role` (Enum: Admin, Realtor, Affiliate, Client)

## Property

Represents a real estate property.

- **Attributes**:
    - `PropertyID` (Primary Key)
    - `Name` (String)
    - `Description` (Text)
    - `Price` (Decimal)
    - `Location` (String)
    - `Images` (JSON array of URLs)
    - `RealtorID` (Foreign Key to User)

## Lead

Represents a potential client interested in a property.

- **Attributes**:
    - `LeadID` (Primary Key)
    - `Name` (String)
    - `Email` (String)
    - `Phone` (String)
    - `PropertyID` (Foreign Key to Property)
    - `RealtorID` (Foreign Key to User)
    - `Status` (Enum: New, Contacted, Closed)

## Enquiry

Represents a question or message from a Client about a property.

- **Attributes**:
    - `EnquiryID` (Primary Key)
    - `Message` (Text)
    - `PropertyID` (Foreign Key to Property)
    - `ClientID` (Foreign Key to User)
    - `Status` (Enum: Pending, Answered)

## AffiliateLink

Represents a unique referral link for an Affiliate.

- **Attributes**:
    - `LinkID` (Primary Key)
    - `AffiliateID` (Foreign Key to User)
    - `Code` (String, Unique)
    - `Clicks` (Integer)
    - `Conversions` (Integer)

## Commission

Represents the commission earned by an Affiliate.

- **Attributes**:
    - `CommissionID` (Primary Key)
    - `AffiliateID` (Foreign Key to User)
    - `Amount` (Decimal)
    - `Status` (Enum: Pending, Paid)
    - `ConversionID` (Foreign Key to a conversion event, e.g., a successful sale)

## Payout

Represents a payment made to a Realtor or Affiliate.

- **Attributes**:
    - `PayoutID` (Primary Key)
    - `UserID` (Foreign Key to User)
    - `Amount` (Decimal)
    - `Date` (DateTime)
    - `Status` (Enum: Pending, Completed, Failed)
    - `Method` (String, e.g., PayPal, Bank Transfer)
