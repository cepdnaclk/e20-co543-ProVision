import axios from "axios";

// Base API of the server
//const API_BASE_URL = import.meta.env.VITE_IMAGE_SERVER_URL;
const API_BASE_URL = "http://localhost:5000/";

// Get data from backend
export async function getData(page: string) {
  try {
    const destination = `${API_BASE_URL}/${page}`;
    //console.log(`Fetching data from: ${destination}`);
    const response = await axios.get(destination);
    return response;
  } catch (error) {
    console.error("There was an error fetching the data!", error);
    throw error;
  }
}

// Send image to the backend and get enhanced image
export async function sendData(sendData: object, page: string) {
  try {
    const destination = `${API_BASE_URL}/${page}`;
    //console.log(`Adding new data in: ${destination}`);

    const response = await axios.post(destination, sendData, {
      responseType: "blob",
    });

    return response;
  } catch (error) {
    console.error("Adding data error!", error);
    throw error;
  }
}

// Delete data in backend
export async function deleteData(sendData: object, page: string) {
  try {
    const destination = `${API_BASE_URL}/${page}`;
    //console.log(`Deleting excisting data in: ${destination}`);
    const response = await axios.delete(destination, { data: sendData });
    console.log("Response: ", response);
    return response;
  } catch (error) {
    console.error("Deleting data error!", error);
    throw error;
  }
}
