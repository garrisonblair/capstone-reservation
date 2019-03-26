import React, { Component } from 'react';
import Navigation from '../Navigation';
import EmailSettings from './EmailSettings';
import PersonalSettings from './PersonalSettings';


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
        <PersonalSettings />
      </div>
    );
  }
}

export default UserSettings;
