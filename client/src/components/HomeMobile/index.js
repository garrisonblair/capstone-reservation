import React, { Component } from 'react';


class HomeMobile extends Component {
  componentDidMount = () => {
    document.title = 'Home';
  }

  render() {
    return (
      <h1> Mobile Home </h1>
    );
  }
}

export default HomeMobile;
