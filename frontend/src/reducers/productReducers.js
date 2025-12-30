import { 
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS,
    PRODUCT_LIST_FAIL,

    PRODUCT_DETAILS_REQUEST,
    PRODUCT_DETAILS_SUCCESS,
    PRODUCT_DETAILS_FAIL
 } from '../constants/productConstants';

// The reducer manages the state of the product list based on the action type
export const productListReducer = (state = { products: [] }, action) => {
    switch (action.type) {
        // While waiting for data from the server
        case PRODUCT_LIST_REQUEST:
            return { loading: true, products: [] }

        // When data is successfully retrieved
        case PRODUCT_LIST_SUCCESS:
            return { loading: false, products: action.payload }
        
        // When the server returns an error
        case PRODUCT_LIST_FAIL:
            return { loading: false, error: action.payload } 
            
        // If none of the above match, return current state
        default:
            return state    
    }
}


export const productDetailsReducer = (state = { product: {reviews: []} }, action) => {
    switch (action.type) {
        // While waiting for data from the server
        case PRODUCT_DETAILS_REQUEST:
            return { loading: true, ...state }
        // When data is successfully retrieved
        case PRODUCT_DETAILS_SUCCESS:
            return { loading: false, product: action.payload }
        
        // When the server returns an error
        case PRODUCT_DETAILS_FAIL:
            return { loading: false, error: action.payload } 
            
        // If none of the above match, return current state
        default:
            return state    
    }
}
