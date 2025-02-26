import api from './api';

// Get all maps
export const getMaps = async () => {
  try {
    const response = await api.get('/maps');
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Get a single map by ID
export const getMapById = async (id) => {
  try {
    const response = await api.get(`/maps/${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Get maps by game mode
export const getMapsByGameMode = async (gameMode) => {
  try {
    const response = await api.get(`/maps/gamemode/${gameMode}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Search maps
export const searchMaps = async (searchTerm) => {
  try {
    const response = await api.get(`/maps/search/${searchTerm}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Create a new map (admin/moderator only)
export const createMap = async (mapData) => {
  try {
    const response = await api.post('/maps', mapData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Update a map (admin/moderator only)
export const updateMap = async (id, mapData) => {
  try {
    const response = await api.put(`/maps/${id}`, mapData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Delete a map (admin only)
export const deleteMap = async (id) => {
  try {
    const response = await api.delete(`/maps/${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
}; 