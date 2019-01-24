/* eslint-disable no-console */
/* eslint-disable react/prefer-stateless-function */
/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import {
  Icon,
} from 'semantic-ui-react';
import api from '../../utils/api';


class UserInfo extends Component {
  state = {
    user: {},
  }

  componentDidMount() {
    api.getMyUser()
      .then((response) => {
        const { data: user } = response;
        console.log(user);
        this.setState({ user });
      });
  }

  renderSecondaryEmail = () => {
    const { user } = this.state;
    let component = '';

    // Empty or no secondary email
    if (!Object.keys(user).length || !user.booker_profile.secondary_email) {
      return component;
    }
    component = (
      <h3>
        <Icon name="envelope outline" />
        {user.booker_profile.secondary_email}
      </h3>
    );
    return component;
  }

  render() {
    const { user } = this.state;
    return (
      <div>
        <h1> User Information </h1>
        <h3>
          <Icon name="user" />
          {user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` : `${user.username}`}
        </h3>
        <h3>
          <Icon name="mail" />
          {user.email}
        </h3>
        {this.renderSecondaryEmail()}
      </div>
    );
  }
}

export default UserInfo;
