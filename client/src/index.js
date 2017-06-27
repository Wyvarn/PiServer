import React from 'react';
import { render } from 'react-dom';
import App from './components/App';
import registerServiceWorker from './registerServiceWorker';
import configureStore from './store/configureStore'
import './styles/css/index.css';
import './styles/css/App.css';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';

const store = configureStore();

render(
    <Provider store={store}>
        <BrowserRouter basename="/">
            <App/>
        </BrowserRouter>
    </Provider>,
    document.getElementById('root')
);

registerServiceWorker();
