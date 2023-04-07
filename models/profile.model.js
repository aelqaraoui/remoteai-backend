const mongoose = require('mongoose');

const ProfileSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
  },
  education: String,
  skills: String,
  workExperience: String,
  achievements: String,
  interests: String,
});

module.exports = mongoose.model('Profile', ProfileSchema);
