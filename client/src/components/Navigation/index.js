import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
// import PropTypes from 'prop-types';


// eslint-disable-next-line react/prefer-stateless-function
class Navigation extends Component {
  render() {
    return (
      <div>
        <h1> Nav </h1>
      </div>
    );
  }
}

export default withRouter(Navigation);
