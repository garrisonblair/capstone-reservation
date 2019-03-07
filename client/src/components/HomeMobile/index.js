import React, { Component } from 'react';

import { Button } from 'semantic-ui-react';

import storage from '../../utils/local-storage';
import LoginComponent from '../Login/login';


class HomeMobile extends Component {
  componentDidMount = () => {
    document.title = 'Home';
  }

  render() {
    const user = storage.getUser();

    return (
      <div>
        <h1> Mobile Home </h1>
        <Button> My Button </Button>
        { user ? null : <LoginComponent /> }
      </div>
    );
  }
}

export default HomeMobile;
