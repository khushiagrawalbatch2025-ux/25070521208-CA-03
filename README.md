# neel – Y2K online shop (FLEXI project)
React (Vite) + Node/Express + MongoDB (Compass)

## Run
1. Start MongoDB, connect Compass to `mongodb://127.0.0.1:27017` (database `neel` appears after seeding).
2. Backend: `cd server && npm install && npm run seed && npm start`
3. Frontend: `cd client && npm install && npm run dev` → open http://localhost:5173

Products load from MongoDB; orders from checkout are saved in the `orders` collection.
