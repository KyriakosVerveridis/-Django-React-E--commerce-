import axios from "axios"
import {
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS,
    PRODUCT_LIST_FAIL,

    PRODUCT_DETAILS_REQUEST,
    PRODUCT_DETAILS_SUCCESS,
    PRODUCT_DETAILS_FAIL
} from "../constants/productConstants"

/**
 * Action Creator to fetch the product list from the API.
 * Uses Redux Thunk for asynchronous dispatching.
 */
export const listProducts = () => async (dispatch) => {
    try {
        // Step 1: Start the request (Loading state)
        dispatch({ type: PRODUCT_LIST_REQUEST })

        // Step 2: Make the API call to Django
        const { data } = await axios.get("/api/products/")

        // Step 3: Dispatch success with the retrieved data
        dispatch({ type: PRODUCT_LIST_SUCCESS, payload: data })

    } catch (error) {
        // Step 4: Dispatch failure with a specific error message
        dispatch({
            type: PRODUCT_LIST_FAIL,
            payload: error.response && error.response.data.detail
                ? error.response.data.detail  // Error message from Django back-end
                : error.message,
        })
    }
}

export const listProductDetails = (id) => async (dispatch) => {
    try {
        // Step 1: Start the request (Loading state)
        dispatch({ type: PRODUCT_DETAILS_REQUEST })

        // Step 2: Make the API call to Django
        const { data } = await axios.get(`/api/products/${id}`)

        // Step 3: Dispatch success with the retrieved data
        dispatch({ type: PRODUCT_DETAILS_SUCCESS, payload: data })

    } catch (error) {
        // Step 4: Dispatch failure with a specific error message
        dispatch({
            type: PRODUCT_DETAILS_FAIL,
            payload: error.response && error.response.data.detail
                ? error.response.data.detail  // Error message from Django back-end
                : error.message, 
        })
    }
}