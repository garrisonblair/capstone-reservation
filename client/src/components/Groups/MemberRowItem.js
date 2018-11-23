import React, { Component } from 'react';
 import { Button, List } from 'semantic-ui-react';
// import api from '../../utils/api';

class MemberRowItem extends Component {
  state = {
    member:''
  }

  componentDidMount(){
    const { selectedMember } = this.props;
    this.setState({
      member: selectedMember,
    });
  }

  render(){
    const { member } = this.state;
    return(
      <List.Item>
        <List.Content floated='right'>
          <Button>Remove</Button>
        </List.Content>
        <List.Content floated='left'>
          {member}
        </List.Content>
      </List.Item>
    );
  }
}

export default MemberRowItem;
