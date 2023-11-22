# Requirements

Users

- have profile page with these:
  - Profile image
  - Email
  - Date of birth
- can update these ^^ in a profile page (must use Ajax, vue)

> **Vue only needs to be used once the user is authenticated.**

i.e. For authentication, you don't need Vue

**Make sure your submitted application has at least 5 test users and at least 10 items on auction**

Items

- Create item/auction page:
  - users can post items for auction
- List items/auctions page:
  - should have a page listing all the items available (completely ajax)
  - can search items with a keyword (search both title and description)
- Show single item page:
  - item should have:
    - title
    - description
    - starting price
    - picture
    - date/time the auction finishes
    - bid price
    - bid user
    - questions and answers
  - users can bid on an item on this page
  - users can send questions to item owner, owner can respond
    - questions and answers should be displayed publically
- Send email when auction ends:
  - at end of auction, winner receives an email
  - confirms if they want to proceed to buy the item
  - use a temporary gmail account for this

Code requiremnets:

- Need full static type checking
- Python uses type annotations
- Vue uses typescript
