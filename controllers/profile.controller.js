const Profile = require('../models/profile.model');
const User = require('../models/user.model');

exports.createProfile = async (req, res) => {
  try {
    const { userId, education, skills, workExperience, achievements, interests } = req.body;
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    const profile = new Profile({
      user: userId,
      education,
      skills,
      workExperience,
      achievements,
      interests,
    });

    await profile.save();
    res.status(201).json({ message: 'Profile created', profile });
  } catch (error) {
    res.status(500).json({ message: 'Error creating profile', error });
  }
};

exports.updateProfile = async (req, res) => {
  try {
    const { userId } = req.params;
    const { education, skills, workExperience, achievements, interests } = req.body;

    const profile = await Profile.findOneAndUpdate(
      { user: userId },
      { education, skills, workExperience, achievements, interests },
      { new: false }
    );

    if (!profile) {
      return res.status(404).json({ message: 'Profile not found' });
    }

    res.status(200).json({ message: 'Profile updated', profile });
  } catch (error) {
    res.status(500).json({ message: 'Error updating profile', error });
  }
};

exports.getProfileByUserId = async (req, res) => {
  try {
    const { userId } = req.params;

    const profile = await Profile.findOne({ user: userId });

    if (!profile) {
      return res.status(404).json({ message: 'Profile not found' });
    }

    res.status(200).json(profile);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching profile', error });
  }
};