import React, { Component } from 'react';
import AdminRequired from '../../HOC/AdminRequired';
import RoomStats from './RoomStats';
import '../Admin.scss';


// eslint-disable-next-line react/prefer-stateless-function
class Stats extends Component {
  render() {
    return (
      <div className="stats">
        <RoomStats />
      </div>
    );
  }
}

export default AdminRequired(Stats);
