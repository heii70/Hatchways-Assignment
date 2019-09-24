package main;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class Main {
	
	public static void main(String[] args) throws IOException { 
		
		Map<Integer, Ordernode> orders = new HashMap<Integer, Ordernode>();
		
		BufferedReader orderBr = new BufferedReader(new FileReader("orders.txt"));
		BufferedReader dependenciesBr = new BufferedReader(new FileReader("dependencies.txt"));

		String line;
		
		orderBr.readLine();
		while ((line = orderBr.readLine()) != null) {
          String[] rowVal = line.split(",");
          
          int id = Integer.parseInt(rowVal[0]);
          String name = rowVal[1];
          orders.put(id, new Ordernode(id, name));
		}
       
        dependenciesBr.readLine();
        while ((line = dependenciesBr.readLine()) != null) {
            String[] rowVal = line.split(",");
            
            int id = Integer.parseInt(rowVal[0]);
            int dependencyId = Integer.parseInt(rowVal[1]);
    
            Ordernode order = orders.get(id);
           	
            order.addDependency(orders.get(dependencyId));
        }
        
        orderBr.close();
        dependenciesBr.close();
        
        printOrders(orders);
	}
	
	public static void printOrdersSimple(Map<Integer, Ordernode> orders) {
		for(Ordernode order : orders.values()) {
        	Iterator<Ordernode> it = order.getDependencies().iterator();
        	
        	System.out.print(order.getId() + ", " + order.getName() + ", [");
        	
        	while(it.hasNext()) {
        		Ordernode dependency = it.next();
        		System.out.print(dependency.getId());
        		
        		if(it.hasNext())
        			System.out.print(", ");
        	}
        		
        	System.out.println("]");
        }
	}
	
	public static void printOrders(Map<Integer, Ordernode> orders) {
		for(Ordernode order : orders.values()) {
			printOrder(order, 0);	
        }
	}
		
	public static void printOrder(Ordernode order, int depth) {
    	Iterator<Ordernode> it = order.getDependencies().iterator();
    	String spaces = "";
    	
    	if(depth > 0)
    		spaces = String.format("%"+ 3*depth +"s", " ");
    	
		System.out.println(spaces + "Id: " + order.getId() + ", Name: " + order.getName());
		
		if(it.hasNext())
			System.out.println(spaces + "Dependencies");
		
    	while(it.hasNext()) {
    		Ordernode dependency = it.next();
    		printOrder(dependency, depth+1);
    	}
	}
	
	
	
}