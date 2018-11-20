import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import './SideNav.scss';


class SideNav extends Component {
  render() {
    const {selectedMenu, navConfig, history} = this.props;
    return (
      <div className="admin-nav">
        <ul>
          {navConfig.map(row =>
            <li
            className={selectedMenu === row.menu? 'active': ''}
            onClick={function(){history.push(row.path)}}
            key={row.menu}
            >
            {row.text}
          </li>
          )}
        </ul>
      </div>
    )
  }
}

export default withRouter(SideNav);
