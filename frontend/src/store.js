import { createStore, combineReducers, applyMiddleware } from 'redux'
import { thunk } from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import { productListReducer, productDetailsReducer } from './reducers/productReducers'
import { cartReducer } from './reducers/cartReducers';

const reducer = combineReducers({
  productList: productListReducer, //Handles the state for the product catalog
  productDetails: productDetailsReducer, //Handles the state for a single product
  cart: cartReducer, //Handles the state for the shopping cart
})
// Check if cart items exist in localStorage; if yes, parse the JSON string, otherwise return an empty array
const cartItemsFromStorage = localStorage.getItem('cartItems') ? JSON.parse(localStorage.getItem('cartItems')) : []

/**
 * Initial state of the application when it first loads.
 * We pre-load the cart state with items retrieved from localStorage 
 * to ensure the user's shopping cart persists across page refreshes.
 */
const initialState = {
  cart: { cartItems: cartItemsFromStorage },
}

const middleware = [thunk]

const store = createStore(
  reducer,
  initialState,
  composeWithDevTools(applyMiddleware(...middleware))
)

export default store