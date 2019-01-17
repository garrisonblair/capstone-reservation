import React, { Component } from 'react';
import PropTypes from 'prop-types';

import {
  Dropdown,
} from 'semantic-ui-react';

import api from '../../utils/api';

class UserSearch extends Component {
  state = {
    dropdownUsers: [],
    users: [],
  }

  handleSearchChange = (event) => {
    api.getUsers(
      {
        search_text: event.target.value,
      },
    ).then((response) => {
      const { maxUsers } = this.props;
      const users = response.data.slice(0, maxUsers);
      const dropdownUsers = users.map(user => ({
        key: user.id,
        value: user.id,
        text: user.username,
      }));
      this.setState({ users, dropdownUsers });
    });
  }

  handleSearchConfirm = (event, data) => {
    const { onSelect } = this.props;
    const { users } = this.state;

    const selectedUser = users.filter((user) => {
      if (user.id === data.value) {
        return true;
      }
      return false;
    });
    onSelect(selectedUser[0]);
  }

  render() {
    const { dropdownUsers } = this.state;
    return (
      <div>
        <Dropdown
          placeholder="Booker"
          fluid
          search
          selection
          options={dropdownUsers}
          onSearchChange={this.handleSearchChange}
          onChange={this.handleSearchConfirm}
        />
      </div>

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
