import React, { Component } from 'react';
import './Calendar.scss';


class Header extends Component {
  state = {
    headerList: [],
    headerNum: 0,
    type: 'column',
    name: 'room',
  }

  static getDerivedStateFromProps(props, state) {
    if (props.headerList === state.headerList && props.type === state.type) {
      return null;
    }
    return {
      headerList: props.headerList,
      headerNum: props.headerList.length,
      type: props.type,
      name: props.name,
    };
  }

  setStyle() {
    const { headerNum, type } = this.state;
    let style;
    if (type === 'column') {
      style = {
        cell: {

        },
        wrapper: {
          gridTemplateColumns: `repeat(${headerNum}, 1fr)`,
          gridColumnStart: 2,
          top: 0,
        },
      };
    } else {
      style = {
        cell: {
          minHeight: '60px',
        },
        wrapper: {
          gridTemplateRows: `repeat(${headerNum}, 1fr)`,
          left: 0,
        },
      };
    }
    return style;
  }

  render() {
    const { headerList, name } = this.state;
    const header = headerList.map(h => (
      <div className={`calendar__${name}s__${name}`} style={this.setStyle().cell} key={h.name ? h.name : h}>
        {h.name ? h.name : h}
      </div>
    ));

    return <div className={`calendar__${name}s__wrapper`} style={this.setStyle().wrapper}>{header}</div>;
  }
}

export default Header;
