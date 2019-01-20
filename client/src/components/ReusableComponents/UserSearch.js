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
        text: `${user.first_name} ${user.last_name} (${user.username})`,
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

    this.setState({ selectedUser: data.value });
    onSelect(selectedUser[0]);
  }

  handleClickClear = () => {
    const { onSelect } = this.props;
    this.setState({ selectedUser: null });
    onSelect(null);
  }

  render() {
    const { dropdownUsers, selectedUser } = this.state;
    return (
      <div className="modal-description">
        <Dropdown
          placeholder="Booker"
          search
          selection
          options={dropdownUsers}
          onSearchChange={this.handleSearchChange}
          onChange={this.handleSearchConfirm}
          value={selectedUser}
        />
        <Button icon onClick={this.handleClickClear}>
          <Icon name="close" />
        </Button>
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
