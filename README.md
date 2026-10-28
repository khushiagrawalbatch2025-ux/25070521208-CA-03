# neel ✦ Y2K Online Shopping Website

FLEXI CA - 03 | 
Name- khushi Agrawal | 
PRN - 25070521208 | 
IIIrd Sem sec - D1 

**neel** is a full-stack online shopping web application built for the **FLEXI project**. Customers can browse products, add them to a cart and place an order. All products and orders are stored in and read from **MongoDB**. The UI follows a **Y2K (late 90s / early 2000s)** aesthetic.

---

## Tech Stack (What We Used)

| Layer | Technology | Why / Where it is used |
|---|---|---|
| Frontend | **HTML, CSS, JavaScript** | Page structure, Y2K styling and logic |
| Frontend library | **React.js 18** | Component-based UI, `useState` for cart and form, `useEffect` to fetch products |
| Build tool | **Vite** | Fast dev server, and a proxy that forwards `/api` calls to the backend (avoids CORS issues in development) |
| Backend | **Node.js** | JavaScript runtime for the server |
| Backend framework | **Express.js** | REST API routes and JSON handling |
| Database | **MongoDB** | NoSQL database storing products and orders |
| ODM | **Mongoose** | Schemas, validation and queries for MongoDB |
| DB GUI | **MongoDB Compass** | View, verify and edit the stored data visually |
| Middleware / config | **cors**, **dotenv** | Cross-origin requests; keeping the port and DB URL in a `.env` file |
| Fonts | **Google Fonts** (Rubik Bubbles, Fredoka) | Bubbly Y2K typography |

---

## Features

- Product listing fetched live from MongoDB
- Add to cart, increase/decrease quantity, live total
- Checkout form (name, email, address) with validation
- Orders saved permanently in MongoDB
- Server recalculates the total from database prices, so the client cannot tamper with prices
- Order confirmation with order ID
- Responsive layout (works on mobile) and keyboard-focus styles
- Y2K design: gradients, glossy buttons, old-OS window frames, sparkles, scrolling banner

---

## Project Structure

```
neel/
├── server/
│   ├── index.js          # Express app, API routes, MongoDB connection
│   ├── seed.js           # Fills the database with sample products
│   ├── models/
│   │   ├── Product.js    # Product schema
│   │   └── Order.js      # Order schema
│   ├── .env              # PORT and MONGO_URI
│   └── package.json
└── client/
    ├── index.html
    ├── vite.config.js    # React plugin + /api proxy to port 5000
    ├── package.json
    └── src/
        ├── main.jsx      # React entry point
        ├── App.jsx       # Products, cart, checkout
        └── styles.css    # Y2K theme
```

---

## How Frontend and Backend Are Connected

```
React (port 5173)  --fetch /api/...-->  Vite proxy  -->  Express (port 5000)  -->  Mongoose  -->  MongoDB (port 27017)
```

1. On page load, React calls `GET /api/products`. Express reads the `products` collection and returns JSON.
2. The user fills the cart (kept in React state).
3. On checkout, React sends `POST /api/orders` with the customer details and cart item IDs and quantities.
4. Express looks up each product in MongoDB, calculates the total, saves the order and returns it.
5. React shows the confirmation message.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products` | Get all products (optional `?category=Clothing`) |
| POST | `/api/orders` | Place an order |
| GET | `/api/orders` | List orders, newest first (optional `?email=...`) |

**Example `POST /api/orders` body**
```json
{
  "customer": { "name": "Neel", "email": "neel@example.com", "address": "Nagpur" },
  "items": [{ "id": "<productId>", "qty": 2 }]
}
```

---

## Database Design (database: `neel`)

**products**: `name`, `price`, `category`, `emoji`, `description`

**orders**: `customer { name, email, address }`, `items [ { product, name, price, qty } ]`, `total`, `createdAt`, `updatedAt`

Order items store a copy of the name and price at purchase time, so old orders stay correct even if the product price changes later.

---

## Setup and Run

**Prerequisites:** Node.js (v18+), MongoDB Community Server, MongoDB Compass.

1. **Start MongoDB** and connect Compass to `mongodb://127.0.0.1:27017`.
2. **Backend**
   ```bash
   cd server
   npm install
   npm run seed     # inserts sample products
   npm start        # API on http://localhost:5000
   ```
3. **Frontend** (in a new terminal)
   ```bash
   cd client
   npm install
   npm run dev      # open http://localhost:5173
   ```
4. In Compass, open the `neel` database to see the `products` and `orders` collections. A new order appears in `orders` right after checkout.

To use MongoDB Atlas instead, change `MONGO_URI` in `server/.env`.

---

## Y2K Design Notes

- **Palette:** baby blue, lilac, hot pink, silver
- **Typography:** Rubik Bubbles for the logo, Fredoka for body text
- **Style elements:** chrome-outlined logo, window title bars (`products.exe`, `cart.exe`), hard offset shadows, glossy pill buttons, sparkle stars, scrolling announcement banner
- Motion is limited to the banner and respects `prefers-reduced-motion`

---

## Future Improvements

- User login and signup (JWT)
- Product search, category filters and product detail pages
- Admin panel to add, edit and delete products
- Payment gateway integration
- Order history page for customers
