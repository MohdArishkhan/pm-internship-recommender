import { clerkClient, getAuth } from "@clerk/express";

// Get current user
export const getCurrentUser = async (req, res) => {
	try {
		const { userId } = getAuth(req);

		if (!userId) {
			return res.status(401).json({
				success: false,
				message: "Unauthorized - No user found",
			});
		}

		const user = await clerkClient.users.getUser(userId);

		return res.status(200).json({
			success: true,
			user: {
				id: user.id,
				email: user.emailAddresses[0]?.emailAddress,
				firstName: user.firstName,
				lastName: user.lastName,
				imageUrl: user.imageUrl,
				username: user.username,
			},
		});
	} catch (error) {
		console.error("Error fetching user:", error);
		return res.status(500).json({
			success: false,
			message: "Internal server error",
		});
	}
};

// Get user profile
export const getUserProfile = async (req, res) => {
	try {
		const { userId } = getAuth(req);

		if (!userId) {
			return res.status(401).json({
				success: false,
				message: "Unauthorized",
			});
		}

		const user = await clerkClient.users.getUser(userId);

		return res.status(200).json({
			success: true,
			profile: {
				id: user.id,
				email: user.emailAddresses[0]?.emailAddress,
				firstName: user.firstName,
				lastName: user.lastName,
				imageUrl: user.imageUrl,
				username: user.username,
				createdAt: user.createdAt,
				lastSignInAt: user.lastSignInAt,
			},
		});
	} catch (error) {
		console.error("Error fetching user profile:", error);
		return res.status(500).json({
			success: false,
			message: "Internal server error",
		});
	}
};

// Update user profile
export const updateUserProfile = async (req, res) => {
	try {
		const { userId } = getAuth(req);
		const { firstName, lastName, username } = req.body;

		if (!userId) {
			return res.status(401).json({
				success: false,
				message: "Unauthorized",
			});
		}

		const updateData = {};
		if (firstName) updateData.firstName = firstName;
		if (lastName) updateData.lastName = lastName;
		if (username) updateData.username = username;

		const updatedUser = await clerkClient.users.updateUser(userId, updateData);

		return res.status(200).json({
			success: true,
			message: "Profile updated successfully",
			user: {
				id: updatedUser.id,
				email: updatedUser.emailAddresses[0]?.emailAddress,
				firstName: updatedUser.firstName,
				lastName: updatedUser.lastName,
				imageUrl: updatedUser.imageUrl,
				username: updatedUser.username,
			},
		});
	} catch (error) {
		console.error("Error updating user profile:", error);
		return res.status(500).json({
			success: false,
			message: "Internal server error",
		});
	}
};

// Check authentication status
export const checkAuth = async (req, res) => {
	try {
		const { userId } = getAuth(req);

		if (!userId) {
			return res.status(401).json({
				success: false,
				authenticated: false,
				message: "Not authenticated",
			});
		}

		return res.status(200).json({
			success: true,
			authenticated: true,
			userId: userId,
		});
	} catch (error) {
		console.error("Error checking auth:", error);
		return res.status(500).json({
			success: false,
			message: "Internal server error",
		});
	}
};
