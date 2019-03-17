import React, { Component } from 'react';
import { Menu } from 'semantic-ui-react';
import AdminRequired from '../../HOC/AdminRequired';
import RoomStats from './RoomStats';
import ProgramStats from './ProgramStats';
import '../Admin.scss';


// eslint-disable-next-line react/prefer-stateless-function
class Stats extends Component {
  state = {
    activeItem: 'room',
  }

  handleItemClick = (activeItem) => {
    this.setState({
      activeItem,
    });
  }

  renderTab = (activeItem) => {
    const components = {
      room: <RoomStats />,
      program: <ProgramStats />,
    };
    return components[activeItem];
  }

  render() {
    const { activeItem } = this.state;
    return (
      <div className="stats">
        <Menu tabular>
          <Menu.Item name="Room" active={activeItem === 'room'} onClick={() => this.handleItemClick('room')} />
          <Menu.Item name="Program" active={activeItem === 'program'} onClick={() => this.handleItemClick('program')} />
        </Menu>
        {this.renderTab(activeItem)}
      </div>
    );
  }
}

export default AdminRequired(Stats);
