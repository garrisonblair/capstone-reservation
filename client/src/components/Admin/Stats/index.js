import React, { Component } from 'react';
import AdminRequired from '../../HOC/AdminRequired';
import '../Admin.scss';


class Stats extends Component {
  render() {
    return (
      <div className="stats">
        <div>Stats Content</div>
      </div>
    )
  }
}

export default AdminRequired(Stats);
