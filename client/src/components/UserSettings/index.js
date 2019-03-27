import React, { Component } from 'react';
import Navigation from '../Navigation';
import EmailSettings from './EmailSettings';


class UserSettings extends Component {
  state={

  }

  componentDidMount() {
  }

  render() {
    return (
      <div>
        <Navigation />
        <br />
        <br />
        <br />
        <EmailSettings />
      </div>
    );
  }
}

export default UserSettings;
