import React, { Component } from 'react';

import { Button } from 'semantic-ui-react';


class HomeMobile extends Component {
  componentDidMount = () => {
    document.title = 'Home';
  }

  render() {
    return (
      <div>
        <h1> Mobile Home </h1>
        <Button> My Button </Button>
      </div>
    );
  }
}

export default HomeMobile;
