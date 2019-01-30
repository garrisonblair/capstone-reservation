import React, { Component } from 'react';
import {
  Button, List, Icon, Loader, Dimmer,
} from 'semantic-ui-react';
import PropTypes from 'prop-types';

class InvitedRowItem extends Component {
  state = {
    isLoading: false,
  }

  handleDeletion = () => {
    this.setState({ isLoading: true });
    const { deleteFunction, selectedInvitation } = this.props;
    deleteFunction(selectedInvitation.id);
  }

  render() {
    const { isLoading } = this.state;
    const { selectedInvitation, isAdmin } = this.props;
    return (
      <List.Item>
        <List.Content floated="left">
          <h3>
            <Icon name="envelope" />
            {selectedInvitation.invited_booker.username}
          </h3>
        </List.Content>
        <List.Content floated="right">
          {isAdmin === true && isLoading === false ? <Button onClick={this.handleDeletion}>Remove</Button> : ''}
          {/* {isLoading ? <Loader active inline /> : null} */}
        </List.Content>
        <Dimmer active={isLoading} inverted>
          <Loader />
        </Dimmer>
      </List.Item>
    );
  }
}

InvitedRowItem.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  selectedInvitation: PropTypes.object.isRequired,
  deleteFunction: PropTypes.func.isRequired,
  isAdmin: PropTypes.bool.isRequired,
};

export default InvitedRowItem;
