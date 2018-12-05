import React, { Component } from 'react';
import { Button, List } from 'semantic-ui-react';
import PropTypes from 'prop-types';
// import api from '../../utils/api';

class MemberRowItem extends Component {
  state = {
    member: '',
  }

  componentDidMount() {
    const { selectedMember } = this.props;
    this.setState({
      member: selectedMember,
    });
  }

  render() {
    const { member } = this.state;
    return (
      <List.Item>
        <List.Content floated="left">
          <h2>{member}</h2>
        </List.Content>
        <List.Content floated="right">
          <Button>Remove</Button>
        </List.Content>
      </List.Item>
    );
  }
}

MemberRowItem.propTypes = {
  selectedMember: PropTypes.string,
};

MemberRowItem.defaultProps = {
  selectedMember: null,
};

export default MemberRowItem;
