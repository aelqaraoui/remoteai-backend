// index.js
const mongoose = require('mongoose');
const dotenv = require('dotenv');

dotenv.config();
const express = require('express');
const cors = require('cors');

const usersRoutes = require('./routes/user.routes');
const profileRoutes = require('./routes/profile.routes');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 1000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));

mongoose.connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});
mongoose.connection.on('connected', () => {
    console.log('Connected to MongoDB');
});

app.use('/api/users', usersRoutes);
app.use('/api/profile', profileRoutes);