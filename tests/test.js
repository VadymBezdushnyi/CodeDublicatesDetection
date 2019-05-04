function makeFlowStep(sources, sinks, residualCapacity) {
    var queue = sources.slice();
    var used = new Array(graphSize).fill(false);
    var previous = new Array(graphSize).fill(-1);

    sources.forEach(function (source) {
        used[source] = true;
        previous[source] = source;
    });

    while (queue.length > 0) { //BFS
        var current = queue.shift();
        for (var i = 0; i < graphSize; i++) {
            if (residualCapacity[current][i] > 0 && !used[i]) {
                used[i] = true;
                previous[i] = current;
                queue.push(i);
            }
        }
    }

    for (var i = 0; i < sinks.length; i++) { //Find used sink, build path and run next step
        if (!used[sinks[i]]) continue;
        var node = sinks[i];
        var flow = Infinity;
        while (previous[node] != node) {
            flow = Math.min(flow, residualCapacity[previous[node]][node]);
            node = previous[node];
        }

        node = sinks[i];
        var edgeIds = [];
        while (previous[node] != node) {
            residualCapacity[previous[node]][node] -= flow;
            residualCapacity[node][previous[node]] += flow;
            edgeIds.push(edgeId[previous[node]][node]);
            node = previous[node];
        }

        edgeIds.forEach(function (id) {
            var edge = edges.get(Math.abs(id));
            var width = Math.abs(capacity[edge.from][edge.to] - residualCapacity[edge.from][edge.to]);
            var label = (width - flow) + '/' + capacity[edge.from][edge.to] + '\n+' + flow;
            changeEdgeStyle(edge.id, '#33EE33', label, 7, (id > 0), (id < 0))
        });

        setTimeout(function () {
            edgeIds.forEach(function (id) {
                var edge = edges.get(Math.abs(id));
                var width = (capacity[edge.from][edge.to] - residualCapacity[edge.from][edge.to]);
                var label = Math.abs(width) + '/' + capacity[edge.from][edge.to];
                if (width) {
                    changeEdgeStyle(edge.id, '#EE3333', label, 7, (width > 0), (width < 0));
                } else {
                    resetEdgeStyle(edge.id);
                }
            });
        }, 2000);

        setTimeout(makeFlowStep, 3000, sources, sinks, residualCapacity);
        break;
    }
}

function runMaxFlow() {
    resetGraph();
    var residualCapacity = capacity.map(function (array) {
        return array.slice();
    });//COPY

    var sources = [];
    var sinks = [];
    for (var i = 0; i < graphSize; i++) {
        if (nodeTypes[i] == NodeType.FLOW_SOURCE) {
            sources.push(i);
        }
        if (nodeTypes[i] == NodeType.FLOW_SINK) {
            sinks.push(i);
        }
    }
    if (sources.length && sinks.length) {
        setTimeout(makeFlowStep, 500, sources, sinks, residualCapacity);
    }
}