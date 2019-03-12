import React, { Component } from 'react';
import PropTypes from 'prop-types';

import {
  Dropdown, Button, Icon,
} from 'semantic-ui-react';

import api from '../../utils/api';

class UserSearch extends Component {
  state = {
    dropdownUsers: [],
    users: [],
    selectedUser: null,
  }

  handleSearchChange = (event) => {
    api.getUsers(event.target.value).then((response) => {
      const { maxUsers } = this.props;
      const users = response.data.slice(0, maxUsers);
      const dropdownUsers = users.map(user => ({
        key: user.id,
        value: user.id,
        text: `${user.first_name} ${user.last_name} (${user.username})`,
      }));
      this.setState({ users, dropdownUsers });
    });
  }

  handleSearchConfirm = (event, data) => {
    const { onSelect } = this.props;
    const { users } = this.state;

    if (data === '') {
      // Clear field
      this.setState({ selectedUser: null });
      onSelect(null);
      return;
    }

    const selectedUser = users.filter((user) => {
      if (user.id === data.value) {
        return true;
      }
      return false;
    });

    this.setState({ selectedUser: data.value });
    onSelect(selectedUser[0]);
  }

  render() {
    const { dropdownUsers, selectedUser } = this.state;
    return (
      <Dropdown
        fluid
        placeholder="Booker"
        search
        selection
        clearable
        options={dropdownUsers}
        onSearchChange={this.handleSearchChange}
        onChange={this.handleSearchConfirm}
        value={selectedUser}
      />
    );
  }
}

UserSearch.propTypes = {
  maxUsers: PropTypes.number,
  onSelect: PropTypes.func,
};

UserSearch.defaultProps = {
  maxUsers: 8,
  onSelect: () => {},
};

export default UserSearch;
